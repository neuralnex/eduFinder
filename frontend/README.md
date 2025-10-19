# EduFinder Frontend

This is the React frontend for the EduFinder AI-Powered Learning Path System.

## Features

- **Real-time Agent Status** - Shows all active agents and their status
- **Agent Profiles** - Direct links to AgentVerse profiles
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Beautiful gradient design with glassmorphism effects
- **Quick Actions** - Easy access to main features

## Getting Started

### Prerequisites
- Node.js 14+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm start
```

Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Production Build

```bash
npm run build
```

Builds the app for production to the `build` folder.

## Architecture

The frontend connects to the EduFinder backend API to:
- Display agent status and information
- Show agent profile links
- Provide quick access to learning features

## Styling

- **CSS Grid & Flexbox** for responsive layouts
- **Glassmorphism** design with backdrop blur effects
- **Gradient backgrounds** for modern appearance
- **Smooth animations** and hover effects
- **Mobile-first** responsive design

## API Integration

The frontend fetches data from the EduFinder backend:
- Root endpoint (`/`) for system information
- Health check (`/health`) for status monitoring
- Agent profile links for direct access
