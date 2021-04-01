let url = document.location.pathname.slice(-2)
var post = new Vue({
    el: '#post',
    data: {
        post: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/v1/posts/' + url)
        .then(function (response){
            vm.post = response.data;
        })
    }
}
)

