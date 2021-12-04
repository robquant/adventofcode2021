open System.IO

let items =
    System.IO.File.ReadLines "input.txt"
    |> Seq.map int


let part1 items =
    items
    |> Seq.pairwise
    |> Seq.sumBy (fun pair -> if snd pair > fst pair then 1 else 0)

let part2 items =
    items
    |> Seq.windowed 3
    |> Seq.map Seq.sum
    |> part1

printfn "Part 1: %d" (part1 items)
printfn "Part 2: %d" (part2 items)
