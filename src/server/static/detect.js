
const detectUrl = window.location.origin + '/detect';
const updateUrl = window.location.origin + '/train';

function updateModel() {
    console.log("updating model...")
    
    // Draw posted image
    var img = new Image()

    let xhr = new XMLHttpRequest();
    xhr.open('POST', updateUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            console.log(this.response)
            
            img.src = "data:image/jpeg;base64," + this.response
            img.style = "max-width:500px;max-height:500px"
            document.getElementById("srcImg").appendChild(img)
        }
        else {
            console.log("HTTP failure, error code: " + this.status)
        }
    }
    xhr.send()
    //exCanvas.toBlob(postExamplesFile, 'image/jpeg');
}
function searchImage() {
    console.log("Searching image")
    let xhr = new XMLHttpRequest();
    xhr.open('POST', detectUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            console.log(this.response)
            
            img.src = "data:image/jpeg;base64," + this.response
            img.style = "max-width:500px;max-height:500px"
            document.getElementById("srcImg").appendChild(img)
        }
        else {
            console.log("HTTP failure, error code: " + this.status)
        }
    }
    xhr.send()

}

// EVENT

window.onload = () => {

    document.getElementById("updateModel").onclick = () => {
        
        updateModel();
        return false;
    };
    document.getElementById("updateModel").onclick = () => {
        
        updateModel();
        return false;
    };
};