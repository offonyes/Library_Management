async function checkTokens() {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    if (!accessToken || !refreshToken) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/api/token/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: accessToken })
        });

        if (!response.ok) {
            // Token is not valid, redirect to login
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error verifying token:', error);
        window.location.href = '/';
    }
}

export { checkTokens }