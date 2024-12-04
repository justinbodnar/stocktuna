<?php
// Scan current directory for PNG files
$files = glob("*.png");

// Group files by prefix before the first underscore
$groups = [];
foreach ($files as $file) {
	$parts = explode('_', $file, 2);
	$prefix = $parts[0];
	$groups[$prefix][] = $file;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Grouped PNG Images</title>
	<style>
		.toggle-content {
			display: none;
			margin-left: 20px;
		}
		.toggle-button {
			cursor: pointer;
			color: blue;
			text-decoration: underline;
		}
		img {
			width: 100%;
			height: auto;
			margin: 10px 0;
		}
	</style>
	<script>
		document.addEventListener("DOMContentLoaded", function() {
			var buttons = document.querySelectorAll(".toggle-button");
			buttons.forEach(function(button) {
				button.addEventListener("click", function() {
					var id = this.getAttribute("data-target");
					var element = document.getElementById(id);
					element.style.display = (element.style.display === "none" || element.style.display === "") ? "block" : "none";
				});
			});
		});
	</script>
</head>
<body>
	<h1>Grouped PNG Images</h1>
	<?php foreach ($groups as $prefix => $images): ?>
		<div>
			<span class="toggle-button" data-target="<?php echo $prefix; ?>">
				<?php echo htmlspecialchars($prefix); ?>
			</span>
			<div id="<?php echo $prefix; ?>" class="toggle-content">
				<?php foreach ($images as $image): ?>
					<div>
						<img src="<?php echo htmlspecialchars($image); ?>" alt="<?php echo htmlspecialchars($image); ?>">
					</div>
				<?php endforeach; ?>
			</div>
		</div>
	<?php endforeach; ?>
</body>
</html>

