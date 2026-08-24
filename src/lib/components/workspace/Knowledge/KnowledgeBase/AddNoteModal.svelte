<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';
	import dayjs from 'dayjs';

	import Modal from '$lib/components/common/Modal.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { WEBUI_BASE_URL } from '$lib/constants';
	import { searchNotes } from '$lib/apis/notes';
	import { addNoteToKnowledgeById, updateNoteInKnowledgeById } from '$lib/apis/knowledge';
	import { user } from '$lib/stores';

	const i18n = getContext('i18n');

	export let show = false;
	export let knowledgeId = '';

	let notes: any[] = [];
	let selectedNoteId: string = '';
	let loading = false;
	let searching = false;

	let duplicateInfo: { fileId: string; noteId: string } | null = null;
	let showConfirmDialog = false;

	const loadNotes = async () => {
		searching = true;
		try {
			const res = await searchNotes(localStorage.token);
			notes = (res?.items ?? []).map((n: any) => ({
				id: n.id,
				title: n.title,
				content: n.data?.content?.md ?? '',
				created_at: n.created_at,
				updated_at: n.updated_at,
				user_id: n.user_id
			}));
		} catch {
			notes = [];
		}
		searching = false;
	};

	$: if (show) {
		selectedNoteId = '';
		duplicateInfo = null;
		showConfirmDialog = false;
		loadNotes();
	}

	const submitHandler = async () => {
		if (!selectedNoteId) {
			toast.error($i18n.t('Выберите заметку'));
			return;
		}

		loading = true;
		try {
			const res = await addNoteToKnowledgeById(localStorage.token, knowledgeId, selectedNoteId);

			if (res?.duplicate) {
				duplicateInfo = {
					fileId: res.existing_file_id,
					noteId: res.note_id
				};
				showConfirmDialog = true;
				loading = false;
				return;
			}

			toast.success($i18n.t('Заметка добавлена в базу знаний'));
			show = false;
		} catch (e: any) {
			toast.error(typeof e === 'string' ? e : $i18n.t('Ошибка при добавлении заметки'));
		}
		loading = false;
	};

	const confirmUpdate = async () => {
		if (!duplicateInfo) return;

		loading = true;
		try {
			await updateNoteInKnowledgeById(
				localStorage.token,
				knowledgeId,
				duplicateInfo.noteId,
				duplicateInfo.fileId
			);
			toast.success($i18n.t('Заметка обновлена в базе знаний'));
			show = false;
		} catch (e: any) {
			toast.error(typeof e === 'string' ? e : $i18n.t('Ошибка при обновлении'));
		}
		loading = false;
	};

	const getSelectedNote = () => notes.find((n) => n.id === selectedNoteId);
</script>

<Modal size="sm" bind:show>
	<div>
		<div class="flex justify-between dark:text-gray-100 p-4 pb-0">
			<div class="text-lg font-semibold">
				{showConfirmDialog ? $i18n.t('Заметка уже в базе') : $i18n.t('Добавить заметку')}
			</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<XMark className="size-5" />
			</button>
		</div>

		{#if showConfirmDialog}
			<div class="p-4">
				<div class="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-xl border border-amber-200 dark:border-amber-800">
					<div class="text-sm font-medium text-amber-800 dark:text-amber-200">
						{$i18n.t('Эта заметка уже добавлена в базу знаний')}
					</div>
					<div class="text-xs text-amber-600 dark:text-amber-400 mt-1">
						{$i18n.t('Обновить содержимое существующей записи?')}
					</div>
				</div>

				<div class="flex justify-end gap-2 mt-4">
					<button
						class="px-3.5 py-2 bg-white dark:bg-gray-900 dark:text-gray-300 rounded-full text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-800 border border-gray-100 dark:border-gray-800"
						on:click={() => {
							showConfirmDialog = false;
							duplicateInfo = null;
						}}
					>
						{$i18n.t('Отмена')}
					</button>
					<button
						class="px-3.5 py-2 bg-black text-white dark:bg-white dark:text-black rounded-full text-sm font-medium transition {loading
							? 'opacity-50 pointer-events-none'
							: ''}"
						on:click={confirmUpdate}
					>
						{loading ? $i18n.t('Обновление...') : $i18n.t('Обновить')}
					</button>
				</div>
			</div>
		{:else}
			<div class="p-4 flex flex-col gap-2">
				<div class="text-sm text-gray-500 dark:text-gray-400">
					{$i18n.t('Выберите заметку из списка для добавления в базу знаний')}
				</div>

				{#if searching}
					<div class="flex justify-center py-6">
						<div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-gray-400" />
					</div>
				{:else if notes.length === 0}
					<div class="text-center py-6 text-gray-500 text-sm">
						{$i18n.t('У вас пока нет заметок')}
					</div>
				{:else}
					<div class="flex flex-col gap-1 max-h-[300px] overflow-y-auto">
						{#each notes as note}
							<button
								class="text-left p-3 rounded-xl text-sm border transition
								{selectedNoteId === note.id
								? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400'
								: 'border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800'}"
								on:click={() => {
									selectedNoteId = note.id;
								}}
							>
								<div class="font-medium truncate">{note.title}</div>
								{#if note.content}
									<div class="text-gray-500 dark:text-gray-400 text-xs mt-0.5 line-clamp-2">
										{note.content.slice(0, 120)}{note.content.length > 120 ? '...' : ''}
									</div>
								{/if}
							</button>
						{/each}
					</div>
				{/if}
			</div>

			<div class="flex justify-end p-4 pt-0 gap-2">
				<button
					class="px-3.5 py-2 bg-white dark:bg-gray-900 dark:text-gray-300 rounded-full text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-800 border border-gray-100 dark:border-gray-800"
					on:click={() => {
						show = false;
					}}
				>
					{$i18n.t('Отмена')}
				</button>
				<button
					class="px-3.5 py-2 bg-black text-white dark:bg-white dark:text-black rounded-full text-sm font-medium transition {loading || !selectedNoteId
						? 'opacity-50 pointer-events-none'
						: ''}"
					on:click={submitHandler}
				>
					{loading ? $i18n.t('Добавление...') : $i18n.t('Добавить')}
				</button>
			</div>
		{/if}
	</div>
</Modal>
