import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PostList from './components/PostList';
import PostForm from './components/PostForm';
import PostDetail from './components/PostDetail';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <Link to="/" className="logo">Content Moderation Platform</Link>
          <nav className="nav">
            <Link to="/">Posts</Link>
            <Link to="/new">Create New</Link>
          </nav>
        </header>
        
        <main className="content">
          <Routes>
            <Route path="/" element={<PostList />} />
            <Route path="/new" element={<PostForm />} />
            <Route path="/posts/:id" element={<PostDetail />} />
          </Routes>
        </main>
        
        <footer className="app-footer">
          <p>&copy; {new Date().getFullYear()} Content Moderation Platform</p>
        </footer>
      </div>
    </Router>
  );
}

export default App; 