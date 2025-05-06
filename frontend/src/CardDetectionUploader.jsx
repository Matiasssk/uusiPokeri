import React, { useState } from "react";

function CardDetectionUploader({ onDetected }) {
  const [imageFile, setImageFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!imageFile) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("image", imageFile);

    try {
      const res = await fetch("http://localhost:5000/detect", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Detected cards:", data.cards);
      onDetected(data.cards); // callback esim. setBoard tai muu käyttö
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded mb-4">
      <h2 className="text-lg font-semibold">Tunnista kortit kuvasta</h2>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImageFile(e.target.files[0])}
        className="mb-2"
      />
      <button
        onClick={handleUpload}
        disabled={!imageFile || uploading}
        className="bg-green-600 text-white px-3 py-1 rounded"
      >
        {uploading ? "Lähetetään..." : "Lähetä ja tunnista"}
      </button>
    </div>
  );
}

export default CardDetectionUploader;
