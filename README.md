# AI Image Storyteller

**Transform Images into Creative Stories with AI**

A complete web application that analyzes images and generates captions, descriptions, objects, emotions, and creative stories using real AI models.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [AI Models](#ai-models)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Backend API](#backend-api)
  - [React Frontend](#react-frontends)
  - [Legacy Frontend](#legacy-frontend)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

AI Image Storyteller is a full-stack web application that uses state-of-the-art AI models to analyze images and generate creative, engaging stories. The application combines computer vision, natural language processing, and creative writing to transform static images into narrative experiences.

The system uses industry-leading AI models:
- **BLIP** for intelligent image captioning
- **DETR** for accurate object detection  
- **GPT-2** for creative story generation

---

## Features

### 🧠 AI-Powered Analysis
- **Intelligent Captioning**: Generates descriptive image captions using BLIP model
- **Object Detection**: Identifies and lists objects in images with DETR
- **Emotion Recognition**: Analyzes mood and atmosphere of images
- **Scene Understanding**: Contextual analysis of image environments
- **Creative Storytelling**: Generates engaging 5-10 line narratives with GPT-2

### 🎨 Modern Frontend Experience
- **React 18 + TypeScript**: Modern, type-safe frontend development
- **Tailwind CSS**: Beautiful, responsive design system
- **Framer Motion**: Smooth animations and micro-interactions
- **Drag & Drop Upload**: Intuitive image upload interface
- **Real-time Loading States**: Beautiful loading animations during AI processing
- **Copy & Download**: Easy sharing of generated stories

### 🛠️ Technical Excellence
- **FastAPI Backend**: High-performance async Python web framework
- **RESTful API**: Clean, well-documented API endpoints
- **Error Handling**: Comprehensive error management and user feedback
- **File Validation**: Secure file upload with type and size validation
- **CORS Support**: Cross-origin requests for development

---

## AI Models

### Computer Vision Models

| Model | Purpose | Performance |
|-------|---------|-------------|
| **BLIP** | Image Captioning | ~2-3 seconds per image |
| **DETR** | Object Detection | Real-time processing |
| **Custom Logic** | Emotion Analysis | Scene-aware detection |

### Language Model

| Model | Purpose | Output |
|-------|---------|--------|
| **GPT-2 Small** | Story Generation | 5-10 line creative narratives |
| **Enhanced Prompting** | Context-aware stories | Scene-specific content |

### Model Capabilities

✅ **Image Understanding**: Recognizes objects, scenes, and contexts  
✅ **Creative Writing**: Generates coherent, engaging stories  
✅ **Emotion Detection**: Identifies mood and atmosphere  
✅ **Scene Analysis**: Understands environments and settings  
✅ **Fast Processing**: Optimized for quick responses  

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for React frontend)
- pip (Python package manager)
- npm or yarn (Node.js package manager)

### Step 1: Clone or Download

```bash
# Clone the repository
git clone https://github.com/mwaqas7984/AI-Image-to-story-telling.git
cd AI-Image-to-story-telling

# Or download and extract the project
```

### Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

This will install:
- `fastapi` - Modern Python web framework
- `uvicorn` - ASGI server
- `torch` - PyTorch for AI models
- `transformers` - Hugging Face transformers
- `pillow` - Image processing
- And other required dependencies

### Step 3: Frontend Setup

```bash
# Navigate to React frontend
cd frontend-new

# Install Node.js dependencies
npm install

# Or with yarn
yarn install
```

This will install:
- `react` ^18.2.0 - React library
- `typescript` - TypeScript compiler
- `tailwindcss` - CSS framework
- `framer-motion` - Animation library
- `lucide-react` - Icon library

### Step 4: Verify Installation

```bash
# Test backend
python -c "from backend.vision_service import analyze_image; print('Backend installed successfully!')"

# Test frontend (from frontend-new directory)
npm run build
```

---

## Quick Start

### 1. Start the Backend

```bash
# From project root
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 2. Start the Frontend

```bash
# From project root
cd frontend-new
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 3. Use the Application

1. Open `http://localhost:3000` in your browser
2. Upload an image using drag-and-drop or file selection
3. Click "Generate Story" to analyze the image
4. View the generated caption, objects, emotion, and story
5. Copy or download the generated story

---

## Usage

### Backend API

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Analyze Image
```bash
curl -X POST \
  http://localhost:8000/api/image-analyze \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-image.jpg"
```

**Response Format:**
```json
{
  "caption": "A student sitting at a desk, working on a laptop.",
  "summary": [
    "A young person is focused on their work at a wooden desk",
    "The laptop screen shows what appears to be code or documentation",
    "Natural lighting from a window illuminates the workspace"
  ],
  "objects": ["person", "desk", "laptop", "chair", "notebook", "books"],
  "emotion": "focused",
  "story": [
    "In the quiet hours of the morning, Sarah found herself completely absorbed in her project.",
    "The glow of her laptop screen cast a soft blue light across her determined face.",
    "Lines of code scrolled by as she worked through the complex algorithm.",
    "A steaming cup of coffee sat nearby, forgotten in the heat of inspiration."
  ]
}
```

### React Frontend (Recommended)

#### Features
- **Modern UI**: Beautiful, responsive interface
- **Drag & Drop**: Intuitive image upload
- **Real-time Feedback**: Loading states and progress indicators
- **Interactive Results**: Animated display of analysis results
- **Copy & Download**: Easy sharing functionality

#### Components
- `ImageUpload` - Drag-and-drop image upload component
- `LoadingState` - Beautiful loading animations
- `ResultsDisplay` - Comprehensive results display
- `App` - Main application component

#### Development
```bash
cd frontend-new
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

### Legacy Frontend (Original)

#### Files
- `home.html` - Landing page with features
- `index_original.html` - Main AI tool interface
- `about.html` - Project information
- `app.js` - JavaScript functionality
- `styles.css` - Complete styling

#### Usage
```bash
# Open directly in browser
open frontend/home.html

# Or serve with static server
cd frontend && python -m http.server 3000
```

---

## Architecture

### System Overview

```bash
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Models     │
│                 │    │                 │    │                 │
│ React + TS      │◄──►│   FastAPI       │◄──►│ BLIP + DETR     │
│ Tailwind CSS    │    │   Python        │    │ GPT-2           │
│ Framer Motion   │    │   Async         │    │ Transformers    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

```bash
User Uploads Image
       │
       ▼
Frontend Validation
       │
       ▼
Backend API (/api/image-analyze)
       │
       ▼
┌─────────────────────────────────┐
│  Image Analysis Pipeline        │
│                                 │
│  1. BLIP Caption Generation     │
│  2. DETR Object Detection       │
│  3. Emotion Analysis            │
│  4. Scene Understanding         │
│  5. GPT-2 Story Generation      │
└─────────────────────────────────┘
       │
       ▼
Structured Response
       │
       ▼
Frontend Display
```

### Backend Architecture

```bash
backend/
├── main.py                 # FastAPI application, API endpoints
├── vision_service.py       # Main orchestration logic
├── fast_huggingface_service.py  # Image analysis models
├── story_generator.py     # GPT-2 story generation
├── config.py              # Configuration management
└── __init__.py
```

### Frontend Architecture

```bash
frontend-new/
├── src/
│   ├── components/          # React components
│   │   ├── ImageUpload.tsx
│   │   ├── LoadingState.tsx
│   │   └── ResultsDisplay.tsx
│   ├── types/              # TypeScript definitions
│   ├── utils/              # Helper functions
│   ├── App.tsx             # Main app component
│   └── main.tsx            # Entry point
├── package.json            # Dependencies
├── vite.config.ts          # Vite configuration
└── README.md               # Frontend docs
```

---

## Project Structure

```bash
AI-Image-to-story-telling/
├── backend/                 # Python backend
│   ├── main.py             # FastAPI server
│   ├── vision_service.py   # Image analysis orchestration
│   ├── fast_huggingface_service.py  # AI models
│   ├── story_generator.py  # Story generation
│   ├── config.py           # Configuration
│   └── __init__.py
├── frontend-new/           # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Helper functions
│   │   ├── App.tsx        # Main app
│   │   └── main.tsx       # Entry point
│   ├── package.json       # Dependencies
│   ├── vite.config.ts     # Build config
│   └── README.md          # Frontend docs
├── frontend/               # Legacy frontend
│   ├── home.html          # Landing page
│   ├── index_original.html # Main tool
│   ├── about.html         # About page
│   ├── app.js             # JavaScript
│   └── styles.css         # Styling
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

---

## API Documentation

### Endpoints

#### GET `/`
Health check endpoint.

**Response:**
```json
{
  "message": "Image Storyteller API is running!"
}
```

#### GET `/health`
Detailed health check.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

#### POST `/api/image-analyze`
Analyze an uploaded image.

**Request:**
- `file`: Image file (multipart/form-data)
- Content-Type: Must start with `image/`
- Max file size: 10MB

**Response:**
```json
{
  "caption": "A student sitting at a desk, working on a laptop.",
  "summary": [
    "A young person is focused on their work at a wooden desk",
    "The laptop screen shows what appears to be code or documentation",
    "Natural lighting from a window illuminates the workspace"
  ],
  "objects": ["person", "desk", "laptop", "chair", "notebook", "books"],
  "emotion": "focused",
  "story": [
    "In the quiet hours of the morning, Sarah found herself completely absorbed in her project.",
    "The glow of her laptop screen cast a soft blue light across her determined face.",
    "Lines of code scrolled by as she worked through the complex algorithm.",
    "A steaming cup of coffee sat nearby, forgotten in the heat of inspiration."
  ]
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "detail": "File must be an image"
}
```

#### 413 Payload Too Large
```json
{
  "detail": "File size must be less than 10MB"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Failed to analyze image"
}
```

---

## Performance

### Model Performance

| Operation | Average Time | Details |
|-----------|-------------|---------|
| **Image Captioning** | 1-2 seconds | BLIP model processing |
| **Object Detection** | 0.5-1 seconds | DETR model inference |
| **Story Generation** | 2-3 seconds | GPT-2 text generation |
| **Total Analysis** | 3-6 seconds | Complete pipeline |

### System Requirements

#### Minimum Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB+ recommended)
- **Storage**: 2GB+ for models
- **Network**: Stable internet for model downloads

#### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **GPU**: CUDA-compatible (optional, faster processing)
- **Storage**: 5GB+ SSD

### Optimization Tips

- **Model Caching**: Models are cached after first use
- **Batch Processing**: Multiple images processed efficiently
- **Memory Management**: Automatic cleanup of temporary files
- **Async Processing**: Non-blocking API responses

---

## Troubleshooting

### Common Issues

#### "Model download failed"
**Solution**: Check internet connection and try again. Models are downloaded on first run.

#### "File must be an image"
**Solution**: Ensure uploaded file is a valid image format (JPG, PNG, GIF, WebP).

#### "File size must be less than 10MB"
**Solution**: Compress the image or use a smaller file.

#### "Backend connection failed"
**Solution**: Ensure backend is running on `http://localhost:8000`.

#### "Frontend not loading"
**Solution**: Check Node.js installation and run `npm install` in frontend-new directory.

#### "Story generation failed"
**Solution**: This is usually a temporary issue. Try uploading the image again.

### Development Issues

#### Port already in use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --reload --port 8001
```

#### Node modules issues
```bash
cd frontend-new
rm -rf node_modules package-lock.json
npm install
```

#### Python environment issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Performance Issues

#### Slow model loading
- Models are downloaded once and cached
- First run will be slower
- Subsequent runs are much faster

#### Memory usage
- Models use ~2GB RAM when loaded
- Consider closing other applications if needed

---

## License

MIT License

Copyright (c) 2025 AI Image Storyteller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments

- Built with [React](https://reactjs.org/) for the modern frontend
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for the backend
- AI models from [Hugging Face](https://huggingface.co/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Animated with [Framer Motion](https://www.framer.com/motion/)
- Icons by [Lucide](https://lucide.dev/)

---

<div align="center">

**AI Image Storyteller** - Transform Images into Creative Stories

Made with 🧠 for creative AI applications

</div>
