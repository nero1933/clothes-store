import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PrivateRoute = ({ element }) => {
    // Access the authentication state from Redux store
    const { id } = useSelector((state) => state.auth);

    // If the user is not logged in (id is null), redirect to the 404 page
    if (id === null) {
        return <Navigate to="/404" replace />;
    }

    // If the user is authenticated, render the requested component
    return element;
};

export default PrivateRoute;
