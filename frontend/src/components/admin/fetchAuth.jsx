import log from "../../helps/logs.mjs";

const fetchAuth = async () => {
    try {
        const response = await fetch("http://localhost:8000/user/is_auth", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        if (!data.success) {
            window.location.replace("/")
        }
        if (!data.data['is_admin']) {
            window.location.replace("/")
        }
    } catch (error) {
        await log("error", "is_auth", error);
    }
}
export {fetchAuth}