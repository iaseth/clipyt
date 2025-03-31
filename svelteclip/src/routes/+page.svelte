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
			console.log(data);
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

<style>
	td { padding: 12px 16px; }
</style>

<section class="bg-slate-50">
	<header class="bg-blue-500 text-white py-6 text-center">
		<h2>Entries for the Week</h2>
	</header>

	<table>
		<tbody>
			{#each weeklyEntries as entry, index (entry.id)}
				<tr class="border-b border-slate-400">
					<td>{index+1}</td>
					<td class="font-mono">
						{new Date(entry.timestamp*1000).toLocaleDateString("en-UK")}
					</td>
					<td class="font-mono">
						{new Date(entry.timestamp*1000).toLocaleTimeString("en-UK")}
					</td>

					<td>
						<pre class="p-3 text-wrap bg-zinc-900 text-white rounded-md">{entry.content}</pre>
					</td>

					<td>
						<button on:click={() => copyToClipboard(entry.content)}>Copy</button>
					</td>
					<td>
						<button on:click={() => deleteEntry(entry.id)}>Delete</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</section>
