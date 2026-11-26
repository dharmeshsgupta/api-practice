// 







import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

import { submitContactForm } from "../services/contactService";
import type {
    ContactFormData,
    SubmitStatus,
} from "../types/contact";

const initialFormData: ContactFormData = {
    name: "",
    email: "",
    message: "",
};

export default function ConstactForm() {
    const [formData, setFormData] = useState<ContactFormData>(initialFormData);
    const [status, setStatus] = useState<SubmitStatus>("idle");
    const [feedback, setFeedback] = useState("");

    const handleChange = (
        event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        const { name, value } = event.target;

        setFormData((previousData) => ({
            ...previousData,
            [name]: value,
        }))
    };

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setStatus("loading");
        setFeedback("");

        try{
            const response = await submitContactForm(formData);

            setStatus("success");
            setFeedback(response.message);
            setFormData(initialFormData);
        } catch (error) {
            setStatus("error");
            setFeedback(
                error instanceof Error
                    ? error.message
                    : "Something went wrong. Please try again."
            );
        }
    };

    return (
        <section className="form-container">
            <h1>Contact Us</h1>
            <form onSubmit={handleSubmit} noValidate>
                <label htmlFor="name">Name</label>
                <input 
                    id="name"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="message">Message</label>
                <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    minLength={10}
                    maxLength={1000}
                    rows={5}
                />

                <button type="submit" disabled={status === "loading"}>
                    {status === "loading" ? "Sending..." : "Send Message"}
                </button>

                {feedback && (
                    <p className={status === "success" ? "success" : "error"}>
                        {feedback}
                    </p>
                )}
            </form>
        </section>
    );
}