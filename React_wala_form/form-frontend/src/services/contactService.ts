


import type { ContactFormData, ContactFormResponse} from "../types/contact";

const API_URL = import.meta.env.VITE_API_URL;

export async function submitContactForm(
    formData: ContactFormData
): Promise<ContactFormResponse> {
    const response = await fetch(`${API_URL}/api/contact`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    })
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Unable to submit the form.");
    }
    return data as ContactFormResponse;
}