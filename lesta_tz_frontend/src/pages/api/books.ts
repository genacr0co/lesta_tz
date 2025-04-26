import { NextApiRequest, NextApiResponse } from 'next';
import { books, IBookDate, hasAllRequiredFields } from '@/shared/const';

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {

    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Origin', '*'); 
    res.setHeader(
      'Access-Control-Allow-Methods',
      'GET,OPTIONS,PATCH,DELETE,POST,PUT'
    );
    res.setHeader(
      'Access-Control-Allow-Headers',
      'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    const { method, query } = req;

    switch (method) {
        case 'GET':
            // console.log(query)

            const sendAll = query.sendAll === 'true';

            if (sendAll) {
                res.status(200).json(books);
                return;
            }

            //tag filter
            const tagsArray = query['tags[]'];
            const selectedTags = Array.isArray(tagsArray)
                ? tagsArray.map(tag => tag as string)
                : tagsArray
                    ? [tagsArray as string]
                    : [];

            if (selectedTags.length === 0) {
                res.status(200).json([]);
                return;
            }

            const filteredBooks = books.filter(book => {
                if (!hasAllRequiredFields(book)) {
                    return false;
                }

                return selectedTags.length === 0 || selectedTags.some(tag =>
                    book.tags.includes(tag)
                );
            });


            const filterByName = query['filterBy[name]'] as 'price' | 'author' | 'date' | undefined;
            const filterByOrder = query['filterBy[order]'] === 'true' ? -1 : 1; // true is desc ⬇️

            let sortedBooks;

            if (filterByName === 'price') {
                // Sort by price, then by author name if prices are equal
                sortedBooks = filteredBooks.sort((a, b) => {
                    if (a.price !== b.price) {
                        return (a.price! - b.price!) * filterByOrder;
                    }
                    return a.author!.localeCompare(b.author!);
                });
            } else if (filterByName === 'author') {
                // Sort by author name
                sortedBooks = filteredBooks.sort((a, b) =>
                    a.author!.localeCompare(b.author!) * filterByOrder
                );
            } else if (filterByName === 'date') {
                // Sort by publication date, then by author name if dates are equal
                sortedBooks = filteredBooks.sort((a, b) => {
                    if (a.date!.getTime() !== b.date!.getTime()) {
                        return (a.date!.getTime() - b.date!.getTime()) * filterByOrder;
                    }
                    return a.author!.localeCompare(b.author!);
                });
            } else {
                // Default sorting: by price, then by author name, then by date
                sortedBooks = filteredBooks.sort((a, b) => {
                    if (a.price !== b.price) {
                        return a.price! - b.price!; // Ascending by price
                    }
                    const authorComparison = a.author!.localeCompare(b.author!);
                    if (authorComparison !== 0) {
                        return authorComparison; // Alphabetical by author
                    }
                    return a.date!.getTime() - b.date!.getTime(); // Ascending by date
                });
            }

            res.status(200).json(sortedBooks);
            break;

        default:
            res.setHeader('Allow', ['GET']);
            res.status(405).end(`Method ${method} Not Allowed`);
    }
}