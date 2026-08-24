<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Modal from './Modal.svelte';
	import { createBugReport } from '$lib/apis/bug-reports';

	const i18n = getContext('i18n');

	export let show = false;

	let name = '';
	let email = '';
	let category = 'пожаловаться на баг';
	let message = '';
	let photo = '';
	let photoPreview = '';
	let bugTime = '';
	let submitting = false;

	const categories = ['Пожаловаться на баг', 'UI/UX отзыв', 'Предложение'];

	const handlePhotoSelect = (e: Event) => {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;

		if (file.size > 5 * 1024 * 1024) {
			toast.error($i18n.t('Photo must be less than 5MB'));
			return;
		}

		const reader = new FileReader();
		reader.onload = () => {
			photo = reader.result as string;
			photoPreview = reader.result as string;
		};
		reader.readAsDataURL(file);
	};

	const removePhoto = () => {
		photo = '';
		photoPreview = '';
	};

	const toLocalDatetime = (d: Date) => {
		const pad = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
	};

	const handleSubmit = async () => {
		if (!name.trim() || !email.trim() || !message.trim()) {
			toast.error($i18n.t('Please fill in all required fields'));
			return;
		}

		submitting = true;
		try {
			await createBugReport(localStorage.token, {
				name: name.trim(),
				email: email.trim(),
				category,
				message: message.trim(),
				...(photo ? { photo } : {}),
				...(bugTime ? { bug_time: bugTime } : {})
			});
			toast.success($i18n.t('Report submitted successfully'));
			show = false;
			name = '';
			email = '';
			category = 'пожаловаться на баг';
			message = '';
			photo = '';
			photoPreview = '';
			bugTime = '';
		} catch (err) {
			toast.error($i18n.t('Failed to submit report'));
		} finally {
			submitting = false;
		}
	};
</script>

<Modal bind:show size="md">
	<div class="px-6 py-5 w-full flex flex-col gap-4">
		<div class="flex items-center justify-between">
			<div class="text-lg font-medium dark:text-gray-100">
				{$i18n.t('Report a Bug / Feedback')}
			</div>
			<button
				class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition"
				on:click={() => (show = false)}
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
					<path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
				</svg>
			</button>
		</div>

		<div class="flex flex-col gap-3">
			<div>
				<label class="text-sm font-medium dark:text-gray-300">{$i18n.t('ФИО')}</label>
				<input
					type="text"
					bind:value={name}
					placeholder={$i18n.t('Your full name')}
					class="w-full mt-1 px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-850 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500"
				/>
			</div>

			<div>
				<label class="text-sm font-medium dark:text-gray-300">{$i18n.t('Почта')}</label>
				<input
					type="email"
					bind:value={email}
					placeholder={$i18n.t('your@email.com')}
					class="w-full mt-1 px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-850 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500"
				/>
			</div>

			<div>
				<label class="text-sm font-medium dark:text-gray-300">{$i18n.t('К чему относится')}</label>
				<select
					bind:value={category}
					class="w-full mt-1 px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-850 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500"
				>
					{#each categories as cat}
						<option value={cat}>{cat}</option>
					{/each}
				</select>
			</div>

			<div>
				<label class="text-sm font-medium dark:text-gray-300">{$i18n.t('Сообщение')}</label>
				<textarea
					bind:value={message}
					placeholder={$i18n.t('Describe your issue or suggestion...')}
					rows="4"
					class="w-full mt-1 px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-850 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500 resize-none"
				></textarea>
			</div>

			<div>
				<label class="text-sm font-medium dark:text-gray-300">
					{$i18n.t('Фото')} <span class="text-gray-400 font-normal">({$i18n.t('необязательно')})</span>
				</label>
				{#if photoPreview}
					<div class="mt-1 relative inline-block">
						<img src={photoPreview} alt="preview" class="h-24 rounded-lg object-cover border border-gray-200 dark:border-gray-700" />
						<button
							type="button"
							class="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center hover:bg-red-600 transition"
							on:click={removePhoto}
						>
							&times;
						</button>
					</div>
				{:else}
					<input
						type="file"
						accept="image/*"
						on:change={handlePhotoSelect}
						class="w-full mt-1 text-sm text-gray-500 dark:text-gray-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-gray-200 dark:file:bg-gray-700 file:text-gray-700 dark:file:text-gray-300 hover:file:bg-gray-300 dark:hover:file:bg-gray-600"
					/>
				{/if}
			</div>

			<div>
				<label class="text-sm font-medium dark:text-gray-300">
					{$i18n.t('Время бага')} <span class="text-gray-400 font-normal">({$i18n.t('необязательно')})</span>
				</label>
				<input
					type="datetime-local"
					bind:value={bugTime}
					class="w-full mt-1 px-3 py-2 rounded-xl bg-gray-100 dark:bg-gray-850 border border-gray-200 dark:border-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500"
				/>
			</div>
		</div>

		<div class="flex justify-end gap-2 pt-1">
			<button
				class="px-4 py-2 rounded-xl text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-850 transition"
				on:click={() => (show = false)}
			>
				{$i18n.t('Cancel')}
			</button>
			<button
				class="px-4 py-2 rounded-xl text-sm font-medium text-white bg-red-500 hover:bg-red-600 disabled:opacity-50 transition"
				disabled={submitting}
				on:click={handleSubmit}
			>
				{submitting ? $i18n.t('Sending...') : $i18n.t('Send')}
			</button>
		</div>
	</div>
</Modal>
