import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { logInUser } from "../services/logInUserService.js";
import { logoutUser } from "../services/logoutUserService.js";
import { forgotPasswordService } from "../services/forgotPasswordService.js";

const storedAuth = localStorage.getItem("auth");
const initialState = storedAuth
    ? JSON.parse(storedAuth)
    : { id: null, name: "Guest", is_guest: true };

// Async thunk for login
export const logIn = createAsyncThunk(
    "auth/login",
    async ({ email, password }, { rejectWithValue }) => {
        try {
            console.log("logIn");
            const { access_token, id, name, is_guest } = await logInUser(email, password);
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("auth", JSON.stringify({ id, name, is_guest }));
            return { id, name, is_guest };
        } catch (err) {
            console.error("Log in (Redux) error:", err);
                if (err.response) {
                    if (err.response.status === 401) {
                        return rejectWithValue(
                            "Invalid email or password."
                        );
                    }
                    if (err.response.status === 403) {
                        return rejectWithValue(
                            "Your account is not activated, please check your email."
                        );
                    }
                    if (err.response.status === 429) {
                        return rejectWithValue(
                            "Max attempts reached. Check your email or wait 24 hours!"
                        );
                    }
                }
            return rejectWithValue("An unknown error occurred.");
        }
    }
);

// Async thunk for logout
export const logout = createAsyncThunk(
    "auth/logout",
    async () => {
        try {
            await logoutUser();
        } catch (err) {
            console.error("Logout (Redux) error:", err);
        } finally {
            localStorage.removeItem("access_token");
            localStorage.removeItem("auth");
        }

        return { id: null, name: "Guest", is_guest: true };
});

// Async thunk for forgot password
export const forgotPassword = createAsyncThunk(
    "auth/forgotPassword",
    async (email, { rejectWithValue }) => {
        try {
            await forgotPasswordService(email);
            return "If this email is registered, you will receive a password reset link.";
        } catch (err) {
            console.error("Reset Password (Redux) error:", err);
            return rejectWithValue("Something went wrong. Please try again later.");
        }
    }
);

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(logIn.fulfilled, (state, action) => {
                console.log("logIn", action.payload);
                return action.payload;
            })
            .addCase(logIn.rejected, (state, action) => {
                console.error("Login failed:", action.payload);
            })
            .addCase(logout.fulfilled, () => {
                return { id: null, name: "Guest", is_guest: true };
            });
    },
});

export default authSlice.reducer;
