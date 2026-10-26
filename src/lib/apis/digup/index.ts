import { WEBUI_API_BASE_URL } from '$lib/constants';

type DigUpHit = {
	path: string;
	kind: string;
	segment: string;
	segment_id: number;
	score: number;
	modified?: number;
	size?: number;
	info?: Record<string, any>;
	excerpt?: string | null;
	loc?: number | null;
	loc_end?: number | null;
	focus?: number | null;
	cosine?: number;
	keyword_rank?: number;
	z?: number;
};

type DigUpSearch = {
	hits: DigUpHit[];
	strong?: number;
	meaning?: boolean;
	ms?: { embed?: number; search?: number };
	warning?: string;
};

function headers(token: string, accept: string) {
	return {
		Accept: accept,
		'Content-Type': 'application/json',
		authorization: `Bearer ${token}`
	};
}

async function json<T = any>(res: Response): Promise<T> {
	if (!res.ok) throw await res.json();
	return res.json() as Promise<T>;
}

export const digupStatus = async (token: string = '') => {
	let error: any = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/digup/status`, {
		method: 'GET',
		headers: headers(token, 'application/json')
	})
		.then((r) => json(r))
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const digupSearch = async (token: string, form: {
	q: string;
	code?: boolean;
	kinds?: string[];
	limit?: number;
	meaning?: boolean;
}) => {
	let error: any = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/digup/search`, {
		method: 'POST',
		headers: headers(token, 'application/json'),
		body: JSON.stringify(form)
	})
		.then(async (r) => {
			if (!r.ok) throw await r.json();
			return (await r.json()) as DigUpSearch;
		})
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res as DigUpSearch;
};

export const digupText = async (token: string, form: { segment: number; code?: boolean }) => {
	let error: any = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/digup/text`, {
		method: 'POST',
		headers: headers(token, 'application/json'),
		body: JSON.stringify(form)
	})
		.then((r) => json(r))
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const digupRender = async (
	token: string,
	form: { path: string; kind?: string; loc?: number | null; pixels?: number }
) => {
	let error: any = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/digup/render`, {
		method: 'POST',
		headers: headers(token, 'application/json'),
		body: JSON.stringify(form)
	})
		.then((r) => json(r))
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export const digupConfig = async (token: string, form: { roots?: string[]; code_roots?: string[] }) => {
	let error: any = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/digup/config`, {
		method: 'POST',
		headers: headers(token, 'application/json'),
		body: JSON.stringify(form)
	})
		.then((r) => json(r))
		.catch((err) => {
			error = err.detail;
			return null;
		});
	if (error) throw error;
	return res;
};

export type { DigUpHit, DigUpSearch };
