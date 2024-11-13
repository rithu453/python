from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://flipkart.com")
    # other actions...
    browser.close()

# with sync_playwright() as playwright:
#     {run(playwright)}






#     class Solution{
    
#     public static class pair( )
    
#     {
#         int vertex,distance;
        
#         pair(int vertex,int distance)
#         {
#             this.vertex=vertex;
#             this.distance=distance;
#         }
        
#     }
    
    
#     //algorith
#     public static void main dij(int[][] graph,int s)
#     {
#         int N=graph.length;
#         int[] distance = new int[N];
        
        
#     }
    
    
#     public static void main( String args[])
#     {
#         Scanner sc=new Scanner(System.in);
#         int n=sc.nextInt();
#         int[] a=new int[];
#         for(int i=0;i<n^2;i++)
#         {
#             a[i]=sc.nextInt()
#         }
#         System.out.println(toString.a);
        
        
        
#     }
# }