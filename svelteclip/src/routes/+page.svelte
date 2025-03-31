<script lang="ts">
	import { onMount } from 'svelte';
	import { writable, type Writable } from 'svelte/store';
	import dayjs from 'dayjs';

	interface Entry {
		id: string;
		timestamp: number;
		content: string;
	}

	const API_BASE_URL: string = 'http://localhost:5000/';
	const entries: Writable<Entry[]> = writable([]);
	const selectedRange: Writable<'day' | 'week'> = writable('day');
	const selectedDate: Writable<string> = writable(dayjs().format('YYYY-MM-DD'));

	export let weeklyEntries: Entry[] = [];

	async function fetchEntries() {
		const start = dayjs($selectedDate).startOf($selectedRange).unix();
		const end = dayjs($selectedDate).endOf($selectedRange).unix();
		
		try {
			const response = await fetch(`${API_BASE_URL}/entries?start=${start}&end=${end}`);
			const data: Entry[] = await response.json();
			entries.set(data);
			weeklyEntries = data;
		} catch (error) {
			console.error('Failed to fetch entries', error);
		}
	}

	async function deleteEntry(id: string) {
		try {
			const response = await fetch(`${API_BASE_URL}/delete/${id}`, { method: 'DELETE' });
			if (response.ok) {
				setTimeout(fetchEntries, 1000);
			}
		} catch (error) {
			console.error('Failed to delete entry', error);
		}
	}

	function copyToClipboard(content: string) {
		navigator.clipboard.writeText(content).then(() => {
			console.log('Copied to clipboard:', content);
			setTimeout(fetchEntries, 1000);
		}).catch(err => {
			console.error('Failed to copy', err);
		});
	}

	onMount(fetchEntries);

	$: fetchEntries();
</script>

<section class="bg-slate-50">
	<header class="bg-blue-500 text-white py-6 text-center hidden">
		<h2>Entries for the Week</h2>
	</header>

	<section class="bg-zinc-800 space-y-6 px-4 py-16">
		{#each weeklyEntries as entry, index (entry.id)}
			<section class="max-w-3xl mx-auto bg-zinc-950 text-white rounded-md overflow-hidden">
				<header class="flex items-center bg-zinc-900">
					<div class="grow font-mono px-4 pt-1 text-zinc-500">
						<b class="text-yellow-500">#{index+1}</b>
						on <b class="text-red-500">{new Date(entry.timestamp*1000).toLocaleDateString("en-UK")}</b>
						at <b class="text-green-500">{new Date(entry.timestamp*1000).toLocaleTimeString("en-UK")}</b>
					</div>
					<div>
						<button on:click={() => copyToClipboard(entry.content)}>Copy</button>
						<button on:click={() => deleteEntry(entry.id)}>Delete</button>
					</div>
				</header>

				<section>
					<pre class="p-3 text-wrap">{entry.content}</pre>
				</section>
			</section>
		{/each}
	</section>
</section>
