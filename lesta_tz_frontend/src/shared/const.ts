export const TRIGGER = {
    CHANGE_TAG: 'CHANGE_TAG'
}

export interface IBookDate {
    id: number;
    title: string;
    author: string;
    date: Date;
    price: number;
    tags: string[];
}


export const hasAllRequiredFields = (book: any): book is IBookDate => {

    if (book.id == undefined) console.error(`"id" is ${book.id} in: ${JSON.stringify(book)}`)
    if (book.title == undefined) console.error(`"title" is ${book.title} in: ${JSON.stringify(book)}`)
    if (book.author == undefined) console.error(`"author" is ${book.author} in: ${JSON.stringify(book)}`)
    if (book.date == undefined) console.error(`"date" is ${book.date} in: ${JSON.stringify(book)}`)
    if (book.price == undefined) console.error(`"price" is ${book.price} in: ${JSON.stringify(book)}`)

    return (
        book.id !== undefined &&
        book.title !== undefined &&
        book.author !== undefined &&
        book.date instanceof Date &&
        book.price !== undefined &&
        Array.isArray(book.tags)
    );
};

export const books = [
    {
        id: 1,
        title: "Space Oddities: The Mysterious Anomalies Challenging Our Understanding of the Universe",
        author: "Harry Cliff",
        date: new Date(2024, 2, 1),
        price: 542,
        tags: ['Climate change', 'History']
    },

    {
        id: 2,
        title: "Plastic: A Novel",
        author: "Acott Guild",
        date: new Date(2024, 1, 1),
        price: 420,
        tags: ['Climate change', 'Sci-Fi']
    },

    {
        id: 3,
        title: "Hidden Book",
    },

    {
        id: 4,
        title: "H Is for Hope: Climate Change from A to Z",
        author: "Elizabeth Kolbert, illustrations by Wesley Allsbrook",
        date: new Date(2024, 2, 1),
        price: 674,
        tags: ['Technology']
    },

    {
        id: 5,
        title: "The Exquisite Machine: The New Science of the Heart",
        author: "Sian E. Harding",
        date: new Date(2024, 1, 1),
        price: 981,
        tags: ['Biochemistry']
    },

]