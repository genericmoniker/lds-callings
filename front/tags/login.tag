<login>
    <h1>Login</h1>
    <div if={error} class="alert alert-danger" role="alert">
        {error}
    </div>
    <form onsubmit={submit}>
        <div class="form-group">
            <input ref="username" onkeyup={validate} class="form-control" type="text" name="username" placeholder="LDS Account Username">
        </div>
        <div class="form-group">
            <input ref="password" onkeyup={validate} class="form-control" type="password" name="password" placeholder="Password">
        </div>
        <button class="btn btn-primary" disabled={!valid}>Login</button>
    </form>

    <script>
        // There is some built-in validation support for HTML forms, but there
        // isn't broad browser support. See:
        // https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement
        // Also:
        // https://getbootstrap.com/docs/4.0/components/forms/#validation
        this.valid = false
        this.error = null
        this.loggingIn = false

        validate() {
            this.valid = (this.refs.username.value.length > 0 && this.refs.password.value.length > 0)
        }

        submit(e) {
            e.preventDefault()
            this.loggingIn = true
            this.update()
            this.opts.auth.login({
                username: this.refs.username.value,
                password: this.refs.password.value
            })
        }

        this.opts.auth.on('login', function() {
            console.log("ON LOGIN")
            this.loggingIn = false
            this.error = null
            this.update()
        }.bind(this))

        this.opts.auth.on('login-failed', function(error) {
            console.log("ON LOGIN FAILED")
            this.loggingIn = false
            this.error = error
            this.update()  // TODO: Docs imply I don't need this explicitly, but doesn't work without it.
        }.bind(this))
    </script>
</login>
