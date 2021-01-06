// function to extract value from field 'Bath'
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    // iterate thru the 5 Bath buttons
    for (var i in uiBathrooms) {
        // return the value of the checked Bath button
        if (uiBathrooms[i].checked) {
            return parseInt(i) + 1;
        }
    }
    return -1; // Invalid Value
}

// function to extract value from field 'BHK'
function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    // iterate thru the 5 BHK buttons
    for (var i in uiBHK) {
        // return the value of the checked BHK button
        if (uiBHK[i].checked) {
            return parseInt(i) + 1;
        }
    }
    return -1; // Invalid Value
}

// this function is called when the button 'Estimate Price' is clicked
function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    // extract the value of each UI component
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");
  
    // var url = "http://127.0.0.1:5000/predict_home_price"; //Use this if you are NOT using nginx which is first 7 tutorials
    var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    // make a JQuery POST call
    $.post(url, {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    }, function(data, status) {
        // data contains output from the POST call
        console.log(data.estimated_price);
        // display estimated_price from data onto the UI
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
        console.log(status);
    });
}

// this function is called when page is loaded
// with this function, refresh the page at app.html to see the 2
// hard-coded location strings have been replaced by the list of locations
function onPageLoad() {
    console.log( "document loaded" );
    // URL to get location names
    // var url = "http://127.0.0.1:5000/get_location_names"; // Use this if you are NOT using nginx which is first 7 tutorials
    var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

    // make a JQuery GET call and store results in data
    $.get(url, function(data, status) {
        console.log("got response for get_location_names request");
        if (data) {
            // get the list of locations from data
            var locations = data.locations;
            // get a handle to the Location drop-down
            var uiLocations = document.getElementById("uiLocations");
            // clear the drop-down
            $('#uiLocations').empty();

            // iterate thru the location list
            for (var location in locations) {
                // save each location as an option
                var option = new Option(locations[location]);
                // add the option into the drop-down
                $('#uiLocations').append(option);
            }
        }
    });
}

// call onPageLoad when page is loaded
window.onload = onPageLoad;