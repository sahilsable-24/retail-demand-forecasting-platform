const API_BASE_URL = "http://127.0.0.1:8000";

export async function getStores() {
    const response = await fetch(`${API_BASE_URL}/stores`)
    
    if(!response.ok){
        throw new Error(`Failed to fetch the store: ${response.status}`)
    }

    const data = await response.json()
    return data
}

export async function getPredictions(requestBody) {
    const response = await fetch(`${API_BASE_URL}/predict`,{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
        },
        body: JSON.stringify(requestBody)
    })

    if(!response.ok){
        throw new Error(`Failed to submit the prediciton data: ${response.status}`)
    }

    const data = await response.json()
    return data
}