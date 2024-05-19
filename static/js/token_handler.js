// Check token Status
// function isTokenExpired(token) {
//     const decodedToken = jwt_decode(token);
//     const currentTime = Date.now() / 1000;
//     return decodedToken.exp < currentTime;
// }

// Refresh Token
async function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');

    const response = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
        const data = await response.json();
        const newAccessToken = data.access;

        localStorage.setItem('accessToken', newAccessToken);

        return newAccessToken;
    } else {
        console.log('Failed to refresh token');
        return null;
    }
}

export { refreshToken };
