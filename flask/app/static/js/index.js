$('#v1_deploy').click(function() {
    $("#v1_deploy").attr("disabled", true);
    $("#v1_deploy").removeClass("btn-dark");
    $("#v1_deploy").addClass("btn-secondary");
    $.get("/v1_deploy")
    .done(function(response){
        $('#contractAddress').html(`<a href="https://ropsten.etherscan.io/address/${response}" target="_blank">${response}</a>`)
        $("#deployContract").modal("show")
    })
})

$('#v2_deploy').click(function() {
    $("#v2_deploy").attr("disabled", true);
    $("#v2_deploy").removeClass("btn-dark");
    $("#v2_deploy").addClass("btn-secondary");
    $.get("/v2_deploy")
    .done(function(response){
        $('#contractAddress').html(`<a href="https://ropsten.etherscan.io/address/${response}" target="_blank">${response}</a>`)
        $("#deployContract").modal("show")
    })
})

$('#validate').click(function() {
    $.get(`/validate/${$('#validateContract').val()}`)
    .done(function(response){
        $('#validateResponseText').text(response)
        $("#validateResponseModal").modal("show")
    })
})


