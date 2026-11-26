


export type ContactFormData = {
    name: string;
    email: string;
    message: string;
}

export type ContactFormResponse = {
    success: boolean;
    message: string;
}

export type SubmitStatus = "idle" | "loading" | "success" | "error";