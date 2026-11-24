namespace BookDesk.Core;

public class Book
{
    public string Title { get; set; } = string.Empty;
    public string Genre { get; set; } = string.Empty;
    public int Copies { get; set; }
    public decimal Price { get; set; }
    public decimal Total { get; private set; }

    public void RecalcTotal()
    {
        Total = Copies * Price;
    }
}
