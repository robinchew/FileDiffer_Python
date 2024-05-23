%%%-------------------------------------------------------------------
%% @doc file_differ public API
%% @end
%%%-------------------------------------------------------------------

-module(file_differ_app).

-behaviour(application).

-export([start/2, stop/1]).

start(_StartType, _StartArgs) ->
    RootDir = filename:join([code:priv_dir(file_differ), "static"]),
    %%io:format("Serving static files from: ~s~n", [RootDir]), % Log the directory path
    Dispatch = cowboy_router:compile([
        { '_',
          [
            {"/raw", diff_logic_handler, []},
            {"/", cowboy_static, {file, "priv/static/index.html"}},
            {"/[...]", cowboy_static, {dir, RootDir}}
          ]
        }
    ]),
    {ok, _} = cowboy:start_clear(
        hello_listener,
        [{port, 8080}],
        #{env => #{dispatch => Dispatch}}
    ),
    file_differ_sup:start_link().

stop(_State) ->
    ok.
