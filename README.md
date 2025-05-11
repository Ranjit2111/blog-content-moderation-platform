# AI-Assisted Content Moderation & Publishing Platform

A platform where users can create and publish short blog posts with AI-assisted content moderation to ensure content meets quality standards and community guidelines.

## About the Project

This application combines FastAPI, SQLite, React, and Google's Gemini AI to create a content moderation and publishing platform. Users can write blog posts that are automatically reviewed by an AI moderation service before publishing. The system flags inappropriate content based on keywords, length, or tone.

The moderation workflow is:
1. User creates a draft post
2. User submits the post for review
3. AI moderates the content, checking:
   - Content length (50-2000 characters)
   - Banned words from a curated list
   - Aggressive tone detection using Gemini AI
4. If approved, the post can be published
5. If flagged, user receives feedback on why the post was rejected

## Features

- **Post Management**:
  - Create draft blog posts
  - Edit draft posts before submission
  - View all posts with status filtering
  - Read published posts in a clean, focused interface

- **AI-Powered Moderation**:
  - Advanced tone detection with Gemini AI for nuanced content analysis
  - Basic rule-based checks for content length and banned words
  - Detailed feedback on why content was flagged
  - Automatic fallback to basic rules if AI service is unavailable

- **Status Workflow**:
  - Draft → Review → Approved/Flagged → Published
  - Clear visual indicators of post status
  - Read-only enforcement for published content

- **Developer Tools**:
  - Python SDK for programmatic interaction (via OpenAPI)
  - Complete API documentation
  - Comprehensive test suite

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, Alembic
- **Frontend**: React, React Router, Axios
- **AI**: Google Generative AI (Gemini)
- **Testing**: Pytest, Httpx

## Project Structure

```
app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py     # Database connection & session management
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── moderation.py   # Content moderation logic w/ Gemini AI
│   │   ├── routes.py       # API endpoints
│   │   ├── schemas.py      # Pydantic data validation models
│   │   └── tests.py        # Unit tests
│   ├── migrations/         # Alembic database migrations
│   ├── banned_words.txt    # List of prohibited words
│   ├── .env.example        # Environment variables template
│   ├── alembic.ini         # Alembic configuration
│   └── main.py             # FastAPI application entry point
├── frontend/
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── PostDetail.jsx  # View/edit individual posts
│   │   │   ├── PostForm.jsx    # Create new posts
│   │   │   └── PostList.jsx    # List all posts with filters
│   │   ├── App.css         # Application styles
│   │   ├── App.jsx         # Main React component
│   │   ├── api.js          # API client for backend
│   │   ├── index.css       # Base styles
│   │   └── main.jsx        # React entry point
│   ├── index.html          # HTML template
│   ├── package.json        # npm dependencies and scripts
│   └── vite.config.js      # Vite configuration
├── requirements.txt        # Python dependencies
├── setupdev.bat            # Setup script for Windows
└── runapplication.bat      # Application startup script for Windows
```

## Setup Guide

### Prerequisites

- Python 3.10
- Node.js 20.x or higher
- npm 10.x or higher
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ranjit2111/blog-content-moderation-platform.git
cd blog-content-moderation-platform
```

### Step 2: Set Up Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Navigate to "Get API key" or "API keys" section
4. Create a new API key or use an existing one
5. Copy the API key for the next step

### Step 3: Configure Environment Variables

1. Navigate to the backend directory
2. Copy the example environment file:
   ```
   copy backend\.env.example backend\.env
   ```
3. Open the `.env` file in a text editor
4. Replace `your_gemini_api_key_here` with your actual Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
5. Save and close the file

### Step 4: Run the Setup Script

Run the setup script to install all dependencies and initialize the database:

```
setupdev.bat
```

This script will:
- Create a Python virtual environment
- Install backend dependencies
- Initialize the database with Alembic
- Install frontend dependencies

### Step 5: Run the Application

Start both the backend and frontend servers:

```
runapplication.bat
```

- The backend API will be available at: http://localhost:8000
- The frontend will be available at: http://localhost:5173
- API documentation will be available at: http://localhost:8000/docs

## Using the Application

1. **Create a Post**:
   - Click on "Create New" in the navigation menu
   - Fill in the title and content (minimum 50 characters)
   - Click "Create Draft" to save your post

2. **Edit a Draft**:
   - Navigate to your draft post
   - Click "Edit Draft" to make changes
   - Click "Save Changes" when done

3. **Submit for Review**:
   - Open a draft post
   - Click "Submit for Review"
   - The AI moderation system will analyze your content

4. **Review Results**:
   - If approved, you will see a green "Approved" message
   - If flagged, you will see reasons why your post failed review
   - For flagged posts, edit the content and resubmit

5. **Publish a Post**:
   - Once a post is approved, click "Publish Post"
   - Published posts cannot be edited and are visible to all users

## API Endpoints

- `POST /posts/` - Create a new draft post
- `PATCH /posts/{post_id}` - Update a draft post
- `POST /posts/{post_id}/submit/` - Submit post for review
- `GET /posts/` - List all posts (filter by status)
- `PATCH /posts/{post_id}/publish/` - Publish an approved post
- `GET /posts/{post_id}` - View a specific post

## SDK Usage

Script Overview
The script I've created demonstrates a complete workflow for content moderation and publishing using the API documented in your SDK. Here's what it does:

1. **Creates a draft post:** Sets up initial content that needs moderation
2. **Submits the post for review:** Triggers the content moderation process
3. **Checks the post status:** Verifies whether it was approved or flagged
4. **Updates the post if flagged:** Demonstrates how to revise content that didn't pass moderation
5. **Publishes the post if approved:** Shows the final step in the workflow
6. **Lists posts with different filters:** Demonstrates how to view all posts or filter by status

## Key Components
### Configuration
The script starts by configuring the API client with your server URL (defaults to localhost:8000).

### Error Handling
Comprehensive try/except blocks around each API call ensure robust error handling.

### Workflow Logic
The script includes conditional logic to handle different moderation outcomes:

- If a post is flagged, it updates the content and resubmits
- If a post is approved, it proceeds to publishing
- If still pending approval, it simply reports the current status

### Status Checking
After each operation, the script checks and displays the current status of the post.

## Usage Instructions

- Make sure your moderation API server is running (on port 8000 by default, or modify the host URL)
- Install the SDK dependencies: pip install -e ./moderation_sdk
- Run the script: python content_moderation_demo.py

## Troubleshooting

- **Gemini API Issues**: If you encounter errors with the Gemini API, verify your API key is correct and that you have access to the Gemini models.
- **Database Errors**: If you experience database issues, try deleting the `content.db` file and rerunning `setupdev.bat`.
- **Frontend Connection Errors**: Ensure the backend server is running on port 8000. Check for any CORS issues in the browser console.
- **Setup Script Fails**: Make sure you have the correct Python and Node.js versions installed.
