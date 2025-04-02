import { useQuery } from "@tanstack/react-query";
import { fetchProducts } from "../services/productsService.js";

export const useProducts = () => {
    return useQuery({
        queryKey: ["products"],
        queryFn: fetchProducts,
        staleTime: 1000 * 60 * 5, // Cache data for 5 minutes
    });
};

export default useProducts;
