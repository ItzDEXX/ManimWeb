# ManimWeb

## Overview
ManimWeb is an innovative web application that transforms natural language prompts into dynamic data visualizations. Our platform bridges the gap between human language and data representation, making it easier for users to create compelling visualizations without deep technical knowledge.

## Core Features
- Text-to-Code Generation using LLM models (Llama/Claude)
- Automated Manim code generation for mathematical animations
- Video rendering using Manim library
- Interactive preview system
- Export capabilities in multiple video formats
- Code editing and customization options

## Technical Architecture

### Frontend
- Next.js framework with React
- Real-time preview system
- Code editor with syntax highlighting
- Video player component
- Progress tracking for rendering
- Responsive dashboard design

### Backend (Google Cloud Platform)
- Python-based API service
- LLM integration for code generation
- Manim rendering pipeline
- Video processing and storage
- Queue management for render jobs
- Container orchestration for scaling

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- React (v18 or higher)
- Python (v3.8 or higher) for NLP components

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/manimweb.git

# Install dependencies
cd manimweb
npm install

# Start development server
npm run dev
```

## Team
- Arvind Dhavala
- Arnav Makkar
- Rushil Singha
