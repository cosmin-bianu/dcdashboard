function openConfirmationDialog(itemName, destionationURL) {
    var modal = document.getElementById("confirmation-dialog");
    modal.classList.add("is-active");
    var content= document.getElementById("modal-content-container");
    var confirmationTextNode =  document.createElement("p");
    confirmationTextNode.innerHTML="Sigur vrei să ștergi "
    confirmationTextNode.classList.add("is-size-4","my-4");
    var itemTitle=document.createElement("span");
    itemTitle.classList.add("has-text-weight-bold");
    itemTitle.innerHTML=`${itemName}`;
    confirmationTextNode.appendChild(itemTitle)
    confirmationTextNode.innerHTML += "?";
    var acceptButton = document.createElement("a");
    acceptButton.textContent="Da";
    acceptButton.href=destionationURL;
    acceptButton.classList.add("button", "is-info",  "is-medium");
    var declineButton = document.createElement("button");
    declineButton.onclick=closeConfirmationDialog;
    declineButton.textContent="Nu";
    declineButton.classList.add("button", "is-danger", "mx-3", "is-medium");

    content.appendChild(confirmationTextNode);
    content.appendChild(acceptButton);
    content.appendChild(declineButton);

}

function closeConfirmationDialog(){
    var modal = document.getElementById("confirmation-dialog");
    modal.classList.remove("is-active");
    var content= document.getElementById("modal-content-container");
    content.textContent='';
}