document.getElementById('login-form').addEventListener('submit', handleLogin);

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');

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
        const errorData = await response.json();
        errorElement.innerText = errorData.detail || 'Login failed';
        errorElement.style.display = 'block';
    }
}

export { handleLogin };
