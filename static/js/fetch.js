const fetchGet = async (url) => {
    console.log(url)
    try {
        const res = await fetch(url,
            {
                method: 'GET', headers: { 'Content-Type': 'application/json' }
            })
        const data = await res.json()
        console.log(data)
        return { "ok": true, "data": data }
    } catch (error) {
        return { "ok": false, "data": error }
    }
};

const fetchPost = async (url, data) => {
    console.log(url)
    try {
        const res = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: data instanceof FormData
                    ? data
                    : JSON.stringify(data)
            });
        const post = await res.json()

        return { "ok": true, "data": post }
    } catch (error) {
        return { "ok": false, "data": error }
    }
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}