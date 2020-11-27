$('#add_comment').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");
    add_comment();
});

function add_comment() {
    console.log("create post is working!") // sanity check
};