import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>404 - Page Not Found</h1>
            <p>Sorry, the page you are looking for doesn't exist.</p>
            <Link to="/">Go to Home Page</Link>
        </div>
    );
};

export default NotFoundPage;