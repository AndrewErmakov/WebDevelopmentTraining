var posts = new Vue({
    el: '#posts',
    data: {
        posts: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/v1/posts/')
        .then(function (response){
            vm.posts = response.data;
        })
    }
}
)