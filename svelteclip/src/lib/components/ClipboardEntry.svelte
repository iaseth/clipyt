
<script lang="ts">
	let {
		entry, index,
		copyToClipboard, deleteEntry
	} = $props();

	let date = new Date(entry.timestamp*1000);
</script>

<section class="max-w-3xl mx-auto bg-zinc-950 text-white rounded-md overflow-hidden">
	<header class="flex items-center bg-zinc-900">
		<div class="grow font-mono px-4 pt-1 text-zinc-500">
			<b class="text-yellow-500">#{index+1}</b>
			on <b class="text-red-500">{date.toLocaleDateString('en-UK')}</b>
			at <b class="text-green-500">{date.toLocaleTimeString("en-UK")}</b>
		</div>
		<div>
			<button onclick={() => copyToClipboard(entry.content)}>Copy</button>
			<button onclick={() => deleteEntry(entry.id)}>Delete</button>
		</div>
	</header>

	<section>
		<pre class="p-3 text-wrap">{entry.content}</pre>
	</section>
</section>
