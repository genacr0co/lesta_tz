import {NextApiRequest, NextApiResponse} from 'next';

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


    const { method } = req;

    switch (method) {
        case 'GET':
            // Создаем Set для хранения уникальных тегов
            const uniqueTags = new Set<string>();

            // Перебираем книги и добавляем теги в Set
            books.forEach(book => {
                
                if (!hasAllRequiredFields(book)) {
                    return false;
                }

                book.tags!.forEach(tag => {
                    uniqueTags.add(tag);
                });
            });

            // Преобразуем Set в массив и возвращаем его
            const uniqueTagArray = Array.from(uniqueTags);
            res.status(200).json({
                tags: uniqueTagArray
            });
            break;
        default:
            // Handle other HTTP methods
            res.setHeader('Allow', ['GET']);
            res.status(405).end(`Method ${method} Not Allowed`);
    }
}