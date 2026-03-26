const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const PORT = 3000;

// ── Middleware ──────────────────────────────────────────────
app.use(cors());
app.use(express.json());

// Serve the frontend HTML
app.use(express.static(__dirname));

// Serve generated audio files
app.use("/audio", express.static(path.join(__dirname, "uploads")));

// ── Multer: save uploaded images to /uploads ────────────────
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, path.join(__dirname, "uploads")),
  filename: (req, file, cb) => {
    const unique = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, unique + path.extname(file.originalname));
  },
});

const upload = multer({
  storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith("image/")) cb(null, true);
    else cb(new Error("Only image files are allowed"), false);
  },
  limits: { fileSize: 10 * 1024 * 1024 }, // 10 MB
});

// ── POST /process-notes ─────────────────────────────────────
app.post("/process-notes", upload.single("noteImage"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No image uploaded." });
  }

  const imagePath = req.file.path;
  const speed = req.body.speed || "Normal";

  // Detect python command
  const pythonCmd = process.platform === "win32" ? "python" : "python3";

  const py = spawn(pythonCmd, [
    path.join(__dirname, "processor.py"),
    imagePath,
    speed,
  ]);

  let stdout = "";
  let stderr = "";

  py.stdout.on("data", (d) => (stdout += d.toString()));
  py.stderr.on("data", (d) => (stderr += d.toString()));

  py.on("close", (code) => {
    if (code !== 0) {
      console.error("Python error:", stderr);
      return res.status(500).json({
        error: "Processing failed.",
        detail: stderr,
      });
    }

    // processor.py prints:  extracted_text|audio_file_path
    const parts = stdout.trim().split("|");
    if (parts.length < 2) {
      return res.status(500).json({ error: "Unexpected output from processor." });
    }

    const text = parts[0];
    const audioAbsPath = parts[1];
    const audioFilename = path.basename(audioAbsPath);

    res.json({
      text,
      audioUrl: `http://localhost:${PORT}/audio/${audioFilename}`,
    });
  });
});

// ── Catch-all: serve index.html ─────────────────────────────
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, () => {
  console.log(`\n✅  AudioScribe server running at http://localhost:${PORT}`);
  console.log(`   Open http://localhost:${PORT} in your browser.\n`);
});
