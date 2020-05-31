
const detectUrl = window.location.origin + '/detect';
const updateUrl = window.location.origin + '/train';

let exCanvas = document.getElementById("postedImage")


function updateModel() {
    console.log("updating model...")
    
    // Draw posted image
    var ctx = exCanvas.getContext("2d");
    //var img = document.getElementById("scream");
    var img = new Image()
    //img.src = "https://static.xx.fbcdn.net/images/emoji.php/v9/t46/2/32/1f412.png"
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', updateUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            console.log(this.response)
            

            img.src = "data:image/jpeg;base64," + this.response
            ctx.drawImage(img, 0, 0);
        }
        else {
            console.log("HTTP failure, error code: " + this.status)
        }
    }
    xhr.send()
    //exCanvas.toBlob(postExamplesFile, 'image/jpeg');
}

// EVENT

window.onload = () => {

    document.getElementById("updateModel").onclick = () => {
        
        updateModel();
        return false;
    };
};