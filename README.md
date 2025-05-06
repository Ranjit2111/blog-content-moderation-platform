# Content Moderation & Publishing Platform

A platform where users can create and publish short blog posts with AI-assisted content moderation.

## Features

- Create and edit draft blog posts
- Automatic content moderation with Gemini AI for tone detection
- Publish approved posts
- View posts by status

## Setup

1. **Copy the environment file**

```
copy backend\.env.example backend\.env
```

2. **Add your Gemini API key** to the `.env` file:

```
GEMINI_API_KEY=your_actual_api_key
```

You can get a Gemini API key from the [Google AI Studio](https://ai.google.dev/).

3. **Run the setup script** to install all dependencies:

```
setupdev.bat
```

## Running the Application

Start both the backend and frontend servers:

```
runapplication.bat
```

- Backend API will be available at: http://localhost:8000
- Frontend will be available at: http://localhost:5173

## API Endpoints

- `POST /posts/` - Create a new draft post
- `PATCH /posts/{post_id}` - Update a draft post
- `POST /posts/{post_id}/submit/` - Submit post for review
- `GET /posts/` - List all posts (filter by status)
- `PATCH /posts/{post_id}/publish/` - Publish an approved post
- `GET /posts/{post_id}` - View a specific post

## AI Moderation

The platform uses Gemini AI to detect aggressive tone in content, providing:

- More nuanced tone detection than simple rule-based checks
- Detailed explanations of why content is flagged
- Fallback to basic rules if the API key is not configured

## SDK Usage

```python
from moderation_sdk import ApiClient
from moderation_sdk.api.posts_api import PostsApi

api = PostsApi(ApiClient())
draft = api.create_post({"title": "Test", "content": "Valid content"})
review = api.submit_post_for_review(post_id=draft.id)
if review.status == "approved":
    api.publish_post(post_id=draft.id)
```
