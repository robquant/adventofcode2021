open System

type Direction =
    | UP
    | DOWN
    | FORWARD

type Command = { Direction: Direction; Amount: int }

let parse (line: string) =
    let direction op =
        match op with
        | "up" -> UP
        | "down" -> DOWN
        | "forward" -> FORWARD
        | e -> failwith $"Unknown operation {e}"

    let command (args: string array) =
        { Direction = direction args.[0]
          Amount = int args.[1] }

    command (line.Split(" ", StringSplitOptions.RemoveEmptyEntries))

let program =
    System.IO.File.ReadAllLines($"{__SOURCE_DIRECTORY__}/input.txt")
    |> Array.map parse

let step_part1 pos command =
    let (depth, horizontal) = pos

    match command.Direction with
    | UP -> (depth - command.Amount, horizontal)
    | DOWN -> (depth + command.Amount, horizontal)
    | FORWARD -> (depth, horizontal + command.Amount)

let step_part2 pos command =
    let (depth, horizontal, aim) = pos

    match command.Direction with
    | UP -> (depth, horizontal, aim - command.Amount)
    | DOWN -> (depth, horizontal, aim + command.Amount)
    | FORWARD -> (depth + aim * command.Amount, horizontal + command.Amount, aim)


let (depth1, horizontal1) = program |> Array.fold step_part1 (0, 0)

printfn "Part 1: %d" (depth1 * horizontal1)

let (depth2, horizontal2, _) =
    program |> Array.fold step_part2 (0, 0, 0)

printfn "Part 1: %d" (depth2 * horizontal2)
