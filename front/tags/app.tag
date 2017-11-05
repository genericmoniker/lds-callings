<app>
    <div if={!auth.token} class="container-fluid">
        <login auth={auth}></login>
    </div>
    <div if={auth.token}>
        You"re logged in!
    </div>

    <script>
        // TODO: Split auth into a core module?
        var self = this  // nesting of functions makes it non-obvious how to bind(this)
        this.auth = riot.observable()
        this.auth.token = null
        this.auth.login = function(params) {
            fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(params)
            }).then(function(response) {
                console.log(response)
                switch (response.status) {
                    case 200:
                        response.json().then(function(data) {
                            self.auth.token = data["token"]
                            self.auth.trigger("login")
                        })
                        break
                    case 401:
                        self.auth.trigger("login-failed", "The username or password was incorrect.")
                        break
                    case 403:
                        self.auth.trigger("login-failed", "Your calling doesn't allow you to log in.")
                        break
                    default:
                        self.auth.trigger("login-failed", "There was an unexpected error.")
                        break
                }
            })
        }

        // This is part of the tag logic, not auth itself.
        this.auth.on('login', function() {
            console.log('TOKEN: ' + this.auth.token)
            this.update()
        }.bind(this))

    </script>

</app>