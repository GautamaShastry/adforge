const API = "https://8b1nly37ih.execute-api.us-east-1.amazonaws.com/Prod";

export async function startJob(imageBase64) {
    const response = await fetch(`${API}/start-job`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageBase64 }),
    });
    return response.json();
}

export async function getStatus(jobId) {
    const response = await fetch(`${API}/get-status?jobId=${jobId}`);
    return response.json();
}

export async function pollUntilComplete(jobId, interval = 3000) {
    return new Promise((resolve, reject) => {
        const poll = async () => {
        try {
            const result = await getStatus(jobId);
            if (result.status === "COMPLETED") {
            resolve(result.data);
            } else if (result.status === "FAILED") {
            reject(new Error("Job failed"));
            } else {
            setTimeout(poll, interval);
            }
        } catch (error) {
            reject(error);
        }
        };
        poll();
    });
}