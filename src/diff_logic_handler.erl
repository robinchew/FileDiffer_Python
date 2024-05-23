-module(diff_logic_handler).
-behaviour(cowboy_handler).
-export([init/2]).

init( Req, State ) ->
    {ok, P} = python:start(),
    
    {Status, Response} = 
        try
            Diff = python:call(P, 'python_scripts.diff_logic', 'get_diff_json_from_args', [<<".">>, <<"HEAD^">>, <<"main">>]),
            {200, Diff}
        catch
            error:{python, 'python_scripts.diff_logic.RevisionStringError', Argument, StackTrace} -> error,
                erlang:display(StackTrace),
                erlang:display(Argument),
                {400, ["400 - Invalid input - ", Argument]};
            error:{python, Class, Argument, StackTrace} -> error,
                erlang:display(StackTrace),
                erlang:display(Argument),
                erlang:display(Class),
                {500, <<"500 - Internal server error">>}
        end,
        
    Req_1 = cowboy_req:reply(
        Status,
        #{<<"content-type">> => <<"text/plain">>},
        Response,
        Req
    ),

    python:stop(P),

    {ok, Req, State}.

    
