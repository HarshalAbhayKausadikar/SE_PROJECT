// link - https://us-west-2b.online.tableau.com/t/mediaanalysis/views/MEDIA-ANALYSIS-FINAL/Dashboard1


var viz, workbook, activeSheet;

function initViz() {
	var containerDiv = document.getElementById("tableauViz");
	var url = "https://us-west-2b.online.tableau.com/t/mediaanalysis/views/MEDIA-ANALYSIS-FINAL/Dashboard1"; // Replace with your Tableau dashboard URL
	var options = {
		width: "100%",
		height: "400px",
		hideTabs: true,
		hideToolbar: true,
		onFirstInteractive: function () {
			workbook = viz.getWorkbook();
			activeSheet = workbook.getActiveSheet();
		}
	};
	viz = new tableau.Viz(containerDiv, url, options);
}


// check --not working ?
function refreshDashboard() {
	workbook.getDatasourcesAsync().then(function (dataSources) {
		var dataSource = dataSources[0];
		dataSource.refreshAsync().then(function () {
			console.log("Data source refreshed.");
		});
	});
}


//  Mine --works
function refreshViz()
{
	console.log("REFRESHING.....");
	viz.refreshDataAsync().then(function ()
	{
		console.log("REFRESHED SUCCESSFULLY.....");
	});
	// viz.refreshDashboard();
	// viz.refreshViz();

}


document.addEventListener("DOMContentLoaded", function () {
	initViz();
});
