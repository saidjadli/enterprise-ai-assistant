# API Documentation

## Authentication

### Login

POST `/api/auth/login`

Returns JWT token.

## Chat

POST `/api/ask`

Send user questions and receive generated answers with sources.

## Conversations

GET `/api/conversations`

GET `/api/conversations/{id}`

DELETE `/api/conversations/{id}`

## Documents

POST `/api/documents/upload`

GET `/api/documents/`

DELETE `/api/documents/{filename}`
