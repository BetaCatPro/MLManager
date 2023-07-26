import { toRefs, reactive } from 'vue'
// import { axiosInstance } from '@/http/axios'

export default (options: any) => {
    const { url } = options
    const state = reactive({
        data: {},
        error: false,
        loading: false
    })

    const run = async () => {
        state.error = false
        state.loading = true
        try {
            const result = await fetch(url).then((res) => res.json())
            // const result = await axiosInstance({
            //     url,
            //     params
            // })
            state.data = result
        } catch (e) {
            state.error = true
        }
        state.loading = false
    }

    return {
        run,
        ...toRefs(state)
    }
}
