export default async function Log(level, name, message) {
    await fetch("http://localhost:8000/logs/create",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "level": level,
                "name": name,
                "message": message.toString()
            })
        },
    )
}