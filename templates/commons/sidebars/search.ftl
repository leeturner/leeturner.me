<div class="row">
    <div class="col-md-11 col-md-offset-1 card">
        <h5>Search</h5>
        <form action="//google.com/search" method="get" accept-charset="UTF-8" class="search-form">
            <div class="input-group">
                <input class="form-control" type="search" name="q" />
                <span class="input-group-btn">
                    <button class="btn btn-custom" type="submit"><span class="glyphicon glyphicon-search"></span></button>
                </span>
            </div>
            <input type="hidden" name="q" value="site:${config.site_host}">
        </form>
    </div>
</div>
