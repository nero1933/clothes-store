import { useQuery } from "@tanstack/react-query";
import { fetchProductDetail } from "../services/productDetailService.js";

export const useProductDetail = (slug) => {
    return useQuery({
        queryKey: ["product"],
        queryFn: () => fetchProductDetail(slug),
        staleTime: 1000 * 60 * 5, // Cache data for 5 minutes
    });
};

export default useProductDetail;
