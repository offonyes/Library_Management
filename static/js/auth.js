// auth.js

import { refreshToken } from './token_handler.js';

// Отправка формы логина
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    console.log(email, password)

    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        const accessToken = data.access;
        const refreshToken = data.refresh;

        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);

        window.location.href = '/index';
    } else {
        console.log('Login failed');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

// async function fetchProtectedData() {
//     let accessToken = localStorage.getItem('accessToken'); //
//
//     if (!accessToken || isTokenExpired(accessToken)) {
//         accessToken = await refreshToken();
//         if (!accessToken) {
//             alert('Session expired. Please log in again.');
//             return;
//         }
//     }
//
//     const response = await fetch('/api/protected/', {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${accessToken}`,
//         },
//     });
//
//     if (response.ok) {
//         const data = await response.json();
//         console.log(data);
//     } else if (response.status === 401) {
//         // If the token is still expired even after refresh, force the user to log in again
//         alert('Session expired. Please log in again.');
//     } else {
//         console.log('Failed to fetch protected data');
//     }
// }

export { handleLogin };
