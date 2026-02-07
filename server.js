const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
const multer = require('multer');
const path = require('path');
const fs = require('fs');
// const tesseract = require('node-tesseract-ocr'); // Optional: for local OCR

app.use(express.json()); // Allows server to read JSON bodies

const upload = multer({ dest: 'uploads/' });

// --- THE NEW LOGIC ---

// 1. OCR ROUTE: Reads the uploaded image
const { spawn } = require('child_process');

app.post('/process-notes', upload.single('noteImage'), (req, res) => {
    if (!req.file) return res.status(400).send('No file.');

    const filePath = req.file.path;

    // Run the Python script
    let outputData = "";
    const pythonProcess = spawn('python', ['processor.py', filePath]);

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        const [text, audioFile] = output.split('|');

        res.json({
            text: text,
            audioUrl: `http://localhost:3000/download/${path.basename(audioFile)}`
        });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
        res.status(500).json({ error: "Processing failed" });
    });
});

// Allow the frontend to download the generated MP3
app.use('/download', express.static('uploads'));

// 2. QUIZ ROUTE: Generates 3 MCQs from text
app.post('/process-notes', upload.single('noteImage'), (req, res) => {
    if (!req.file) return res.status(400).send('No file.');

    const filePath = path.resolve(req.file.path);
    
    // CHANGE: Use the path to your 'env' if 'python' doesn't work
    // const pythonPath = path.join(__dirname, 'env', 'Scripts', 'python.exe');
    // Example Node.js snippet
const pythonProcess = spawn('python', ['text_audio.py', req.file.path, req.body.speed]);

    let resultString = "";

    pythonProcess.stdout.on('data', (data) => {
        resultString += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) return res.status(500).json({ error: "Python failed" });

        const parts = resultString.trim().split('|');
        if (parts.length < 2) return res.status(500).json({ error: "Invalid Python output" });

        res.json({
            text: parts[0],
            audioUrl: `http://localhost:3000/download/${path.basename(parts[1])}`
        });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });
});

// 3. AUDIO ROUTE: (Simulation of TTS)
app.post('/generate-audio', (req, res) => {
    // In production, you'd use Google Text-to-Speech API here
    res.json({ audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' });
});

app.listen(3000, () => console.log('Backend running on http://localhost:3000'));