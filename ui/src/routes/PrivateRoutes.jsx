import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux'; // Import useSelector to access Redux state

const PrivateRoute = ({ element, ...rest }) => {
    // Get the user's authentication state from Redux
    const { id } = useSelector((state) => state.auth);

    // If the user is a guest (not logged in), redirect to the login page
    if (id) {
        return <Navigate to="/login" replace />;
    }

    // If the user is authenticated, render the requested component
    return <Route {...rest} element={element} />;
};

export default PrivateRoute;